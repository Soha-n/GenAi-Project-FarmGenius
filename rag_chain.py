from typing import List, Dict, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM
from vector import VectorStore
import time

class FarmGenius:
    def __init__(self, vector_store: Optional[VectorStore] = None):
        """
        Initialize FarmGenius with an optional vector store and LLM.
        Web search is handled via DuckDuckGo (free, no API key required).

        Args:
            vector_store (VectorStore | None): Initialized vector store, or None for LLM-only mode.
        """
        self.vector_store = vector_store

        # Initialize DuckDuckGo search
        try:
            from langchain_community.tools import DuckDuckGoSearchRun
            self.search_tool = DuckDuckGoSearchRun()
            self.search_source = "DuckDuckGo"
            print("Web search: DuckDuckGo initialised.")
        except Exception as e:
            self.search_tool = None
            self.search_source = None
            print(f"DuckDuckGo init failed ({e}). Web search disabled.")

        # Initialize LLM with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.llm = OllamaLLM(
                    model="llama3.2:3b",
                    temperature=0.3,
                )
                self.llm.invoke("test")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to initialize LLM after {max_retries} attempts: {str(e)}")
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2)

        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are FarmGenius, a knowledgeable and friendly agriculture assistant for Indian farmers.
            You specialize in helping farmers with practical, actionable advice on the following topics:
            - Crop Selection: Recommending the right crops based on season, soil type, region, and climate.
            - Soil Health: Advising on soil testing, improving soil fertility, pH management, and organic matter.
            - Weather Guidance: Interpreting weather patterns and giving farming recommendations accordingly.
            - Pest and Disease Control: Identifying common crop pests and diseases and suggesting organic or chemical remedies.
            - Fertilizers and Irrigation: Recommending fertilizer schedules, dosages, and efficient irrigation techniques (drip, sprinkler, flood).
            - Market Price Information: Providing guidance on current market trends, MSP (Minimum Support Price), mandi prices, and when to sell produce.

            You have THREE sources of information — use all of them together:
            1. Agriculture knowledge base (from uploaded documents)
            2. Live web search results
            3. Your own built-in agriculture knowledge

            Prioritise the knowledge base, supplement with web results, and fill gaps with your own expertise.
            Always give practical, easy-to-understand guidance suitable for Indian farmers.
            Use simple language and provide step-by-step instructions when relevant.
            Format your response in a clear, structured way with bullet points or numbered steps where appropriate.
            
            Previous conversation:
            {chat_history}

            Agriculture knowledge base context:
            {context}

            Live web search results:
            {web_context}
            """),
            ("human", "{question}")
        ])

        # Build LCEL chain: prompt | llm | output parser
        self.chain = self.prompt | self.llm | StrOutputParser()
        
    # ------------------------------------------------------------------
    # Web search helper
    # ------------------------------------------------------------------

    def _fetch_web_context(self, query: str) -> str:
        """Run a DuckDuckGo search and return a formatted string of results."""
        if not self.search_tool:
            return "Web search not available."
        try:
            results = self.search_tool.run(f"India farming agriculture {query}")
            return str(results)
        except Exception as e:
            return f"Web search failed: {str(e)}"

    # ------------------------------------------------------------------
    # Context / history formatters
    # ------------------------------------------------------------------

    def _format_context(self, documents: List[Document]) -> str:
        if not documents:
            return "No relevant context found in knowledge base. Providing general agriculture advisory response."
        return "\n\n".join([doc.page_content for doc in documents])

    def _format_chat_history(self, chat_history: List[Dict[str, str]]) -> str:
        if not chat_history:
            return "No previous conversation."
        formatted_history = []
        for msg in chat_history:
            role = "Farmer" if msg["role"] == "user" else "FarmGenius"
            formatted_history.append(f"{role}: {msg['content']}")
        return "\n".join(formatted_history)

    # ------------------------------------------------------------------
    # Main response method
    # ------------------------------------------------------------------

    def get_response(self, query: str, chat_history: List[Dict[str, str]] = None) -> str:
        try:
            # 1. RAG context from the vector store
            if self.vector_store is not None:
                documents = self.vector_store.similarity_search(query)
                context = self._format_context(documents)
            else:
                context = (
                    "No external knowledge base loaded. "
                    "Answer using your comprehensive built-in agriculture knowledge for Indian farmers."
                )

            # 2. Live web search results
            web_context = self._fetch_web_context(query)

            # 3. Generate response combining all three sources
            formatted_history = self._format_chat_history(chat_history or [])
            response = self.chain.invoke({
                "context": context,
                "chat_history": formatted_history,
                "question": query,
                "web_context": web_context
            })

            return response
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your query: {str(e)}. Please try again or rephrase your question." 