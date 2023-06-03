import os
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, \
                        LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI 
from llama_index import StorageContext, load_index_from_storage
import openai

openai.api_key = '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'
os.environ["OPENAI_API_KEY"] = "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"

def index_documents(folder):
    max_input_size    = 4096
    num_outputs       = 512
    max_chunk_overlap = 1
    chunk_size_limit  = 600

    prompt_helper = PromptHelper(max_input_size, 
                                 num_outputs, 
                                 max_chunk_overlap, 
                                 chunk_size_limit = chunk_size_limit)
    
    llm_predictor = LLMPredictor(
        llm = ChatOpenAI(openai_api_key="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", 
                         temperature = 0.7, 
                         model_name = "gpt-3.5-turbo", 
                         max_tokens = num_outputs) # type: ignore
        )

    documents = SimpleDirectoryReader(folder).load_data()

    index = GPTVectorStoreIndex.from_documents(
                documents, 
                llm_predictor = llm_predictor, 
                prompt_helper = prompt_helper)

    index.storage_context.persist(persist_dir="docs") # save in current directory


def my_chatGPT_bot(input_text):
    # load the index from vector_store.json
    storage_context = StorageContext.from_defaults(persist_dir="docs")
    index = load_index_from_storage(storage_context)

    # create a query engine to ask question
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response.response