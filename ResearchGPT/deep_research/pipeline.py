from .agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)
def run_research_pipeline(topic : str ) -> dict:
    state = {}

    # step1 - Search Agent Working

    print("\n" + "=" * 50)
    print("...step1 : search agent working...")
    print("=" * 50)


    serach_agent = build_search_agent()
    search_result = serach_agent.invoke({
        "messages":[("user",f"Find recent,reliable and detailed information about: {topic}")]
    })

    state["search_result"] = search_result["messages"][-1].content

    print("\n search result",state["search_result"]) 


#Step 2 - reader agent
    print("\n" + "=" * 50)
    print("...step1 : scripting top resources...")
    print("=" * 50)


    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
    {
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_result'][:800]}"
            )
        ]
    }
)   

    state["scrapped_content"] = reader_result["messages"][-1].content
    print("\n scripped result",state["scrapped_content"])



    #step 3 : writer chain
    print("\n" + "=" * 50)
    print("...writer chain creating report...")
    print("=" * 50)


    research_combine = (
        f"search result\n {state['search_result']}\n\n"
        f"detailed scrapped result : \n {state["scrapped_content"]}"
    )

    state['report'] = writer_chain.invoke({
        "topic":topic,
        "research":research_combine
    })

    print("\n final report \n",state['report'])



    # step4 - Critic chain Reviewing
    print("\n" + "=" * 50)
    print("...step4 : Critic chain Reviewing...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({"report" : state["report"]})
    print("\n final report \n",state['feedback'])

    return state




if __name__ == "__main__":
    topic = input("\n enter a research topic")
    run_research_pipeline(topic)
