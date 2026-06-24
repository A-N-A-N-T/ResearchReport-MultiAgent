from agents import search_agent , reader_agent , writer_chain , critic_chain
from utils.pdfGenerator import generate_pdf
# from ragConcepts.reportChunking import split_report
# from ragConcepts.vectorStore import create_vectorStore 
# from ragConcepts.retriver import get_retriever



def run_research_pipeline(topic : str) -> dict:
    state = {}

    #print("\n"+"-"*50)
    #print("step 1 - Search agent is working....")
    #print("-"*50)
    
    state["topic"] = topic

    var_search_agent = search_agent()
    search_result = var_search_agent.invoke({
        "messages" : [{"role":"user",
                      "content" : f"Find recent , reliable and detailed information about : {topic}"}]
    })
    state["search_results"] = search_result['messages'][-1].content

    #print("\n search result ",state['search_results'])

    #print("-"*50)
    #print("step 2 - Reader agent is scraping top resources...")
    #print("-"*50)

    var_reader_agent = reader_agent()
    reader_result = var_reader_agent.invoke({
        "messages": [
            {"role" : "user",
             "content" : f"Based on the following search results about {topic} , "
                         f"pick the most recent and matched results for deeper content. \n"
                         f"Search Results : \n {state['search_results'][:800]}"
            }
        ]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    #print("\nscraped content: \n", state['scraped_content'])

    #print("\n"+" -"*50)
    #print("step 3 - Writer is drafting the report ...")
    #print("-"*50)

     
    research_combined = (
        f"Search Results : \n {state['search_results']} \n"
        f"Detailed scraped content : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain().invoke({
        "topic" : topic ,
        "research" : research_combined
    })

    #print("\n Final Report\n",state['report'])

    #critic report 

    #print("\n"+" -"*50)
    #print("step 4 - critic is reviewing the report ")
    #print("-"*50)

    state["feedback"] = critic_chain().invoke({
        "report":state['report']
    })

    #print("\n critic report \n", state['feedback'])

    #################### Rag Implementation ############## 
     
    # # Step 1 - Creating chunks
    
    # chunks = split_report(state["report"])

    # # step 2 - creating embedding and storing chunks into the vectorDB

    # vecStore = create_vectorStore(chunks)
    # state["vectorStore"] = vecStore

    # # step 3 - creating Retreiver 
    # retriever = get_retriever(vecStore)
    # state["retriever"] = retriever

    
    
    return state


def run_research_pipeline_without_RAG(topic : str) -> dict:
    state = {}

  
    
    state["topic"] = topic

    var_search_agent = search_agent()
    search_result = var_search_agent.invoke({
        "messages" : [{"role":"user",
                      "content" : f"Find recent , reliable and detailed information about : {topic}"}]
    })
    state["search_results"] = search_result['messages'][-1].content


    var_reader_agent = reader_agent()
    reader_result = var_reader_agent.invoke({
        "messages": [
            {"role" : "user",
             "content" : f"Based on the following search results about {topic} , "
                         f"pick the most recent and matched results for deeper content. \n"
                         f"Search Results : \n {state['search_results'][:800]}"
            }
        ]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

     
    research_combined = (
        f"Search Results : \n {state['search_results']} \n"
        f"Detailed scraped content : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain().invoke({
        "topic" : topic ,
        "research" : research_combined
    })

 
    state["feedback"] = critic_chain().invoke({
        "report":state['report']
    })


    return state

if __name__ == "__main__":
    topic = input("\n Enter any topic : ")
    run_research_pipeline(topic)

