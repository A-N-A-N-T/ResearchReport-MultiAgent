from final_pipeline import run_research_pipeline_without_RAG
from comparisionChain import compareChain

def compareReport(topicA : str,topicB : str) -> dict:
    reportA_state = run_research_pipeline_without_RAG(topicA)
    reportB_state = run_research_pipeline_without_RAG(topicB)
    response = compareChain().invoke({
        "topic1" : topicA,
        "topic2" : topicB,
        "report1" : reportA_state["report"],
        "report2" : reportB_state["report"]
    })
    return response
