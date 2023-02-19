"""
General Algorithm:
1. Get all the problems from leetcode
    a. Iterate all the pages and insert them into the dB
    b. Iterate all the non-locked problems in the dB and 
       retrieve the content/header from the problem page, then add this content to the dB
2. Get the ChatGPT response
    a. Iterate all the non-locked problems in the dB and format
       the content to use the language and header information, then add the ChatGPT response to the dB
3. Submit the response to leetcode
    a. Iterate all the non-locked problems in the dB and submit the ChatGPT response to leetcode, 
       then record in the dB if it succeeded (get runtime + space used) or failed (get number of test cases it passed)

"""

import os
import logging
from dotenv import load_dotenv
from database_connector import DatabaseConnector
from leetcode_handler import LeetcodeHandler
import openai
from time import sleep
import re
import json


def main():

    logger.info("Starting ChatGPT leetcode problems benchmark...")

    # load the env variables
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "assets", "config", ".env"))

    # create our database connector
    database_connector = DatabaseConnector(
        hostname = os.environ.get("MYSQL_HOSTNAME"),
        username = os.environ.get("MYSQL_USER"),
        password = os.environ.get("MYSQL_PASSWORD"),
        port = os.environ.get("MYSQL_PORT")
    )

    # create our custom leetcode handler
    leetcode_handler = LeetcodeHandler()

    try:

        """Uncomment the functions you are using as each one needs to be manually confirmed it worked before moving to the next"""
        
        # get_leetcode_problems(leetcode_handler, database_connector)
        
        # populate_problem_details(leetcode_handler, database_connector)

        # clean_up_headers_1(database_connector, leetcode_handler)

        # get_openai_responses(database_connector)

        # submit_results(database_connector, leetcode_handler)
        
        # process_results(database_connector, save_results=True)
        
        # save_all_results(database_connector, save_results=True)
        
        pass

    except Exception as e:
        raise e
    finally:
        # clean up our used instances
        # leetcode_handler.close_webdriver()
        database_connector.close()


def get_leetcode_problems(leetcode_handler, database_connector):
    # 1. Get all the problems from leetcode
    # get all the urls of the problem pages
    logger.debug("Getting all problem urls")
    problem_urls = leetcode_handler.get_all_problems_urls()
    # 1.a. Iterate all the pages and insert them into the dB
    for url in problem_urls:
        # get all the problems posted on the problems page
        logger.debug("Scraping problems from page:\n\t%s", url)
        page_results = leetcode_handler.parse_problems(url)
        for problem in page_results:
            # insert the problem into the problem table
            database_connector.insert_into_table(
                table = "ChatGPT.leetcode_benchmark",
                cols = ["title", "problem_number", "problem_url", "acceptance", "difficulty", "locked"],
                values = (
                    problem["title"],
                    problem["problem_number"],
                    problem["problem_url"],
                    problem["acceptance"],
                    problem["difficulty"],
                    problem["locked"],
                ),
                ignore = True,
            )

            # if there are topic tags we will add them to the table
            if problem["topic_tags"]:
                # get the inserted primary key
                primary_key = database_connector.get_last_inserted_primary_key()
                topic_tags_list = [[primary_key, topic] for topic in problem["topic_tags"]]

                # insert the topic tags into the topics table                
                database_connector.insert_into_table(
                    table = "ChatGPT.leetcode_tags",
                    cols = ["problem_id", "topic_tag"],
                    values = topic_tags_list,
                    ignore = True,
                )
        logger.debug("Done scraping problems from page:\n\t%s", url)


def populate_problem_details(leetcode_handler, database_connector):
    # 1.b. Iterate all the non-locked problems in the dB and 
    # retrieve the content/header from the problem page, then add this content to the dB
    logger.debug("Populating the content of each problem")
    scrapped_problems = database_connector.select_from_table(
        table = "ChatGPT.leetcode_benchmark",
        col_choice = "*",
        col = ["locked", "problem_content"],
        value = ["false", None],
        comparison = ["=", "is"],
    )

    for problem in scrapped_problems:
        # need to sleep to not cause leetcode to rate limit timeout
        sleep(5)
        problem_id = problem[0]
        problem_url = problem[3]            

        language = get_desired_language(database_connector, problem_id)

        (problem_header, problem_content) = leetcode_handler.parse_problem_content(problem_url, language)

        database_connector.update_table(
            table = "ChatGPT.leetcode_benchmark",
            cols = ["problem_header", "problem_content"],
            values = [problem_header, problem_content],
            condition = f" WHERE id = {problem_id}"
        )


def get_openai_responses(database_connector):
    """Iterate problems in database and get openai solution"""
    
    logger.debug("Processing OpenAI responses")
    
    # construct openai object
    openai.api_key = os.getenv("OPEN_AI_API_KEY")
    # text-davinci-003 or code-davinci-002 are best options as of 12/30/2022 per https://beta.openai.com/docs/models/overview
    # when manually testing it seemed as though text-davinci-003 was performing much better than code-davinci-002, the solutions were 
    # more succinct and crisp where code-davinci was creating way too many docstrings/comments and additional functions
    # perhaps this was an error with my fine tuning of the parameters but I am not sure if that is the case
    openai_model = "text-davinci-003"   

    # get all the problems from the dB
    problems = database_connector.select_from_table(
        table = "ChatGPT.leetcode_benchmark",
        col_choice = "*",
        col = ["locked", "problem_content", "openai_response"],
        value = ["false", None, None],
        comparison = ["=", "is not", "is"],
    )

    # for each problem
    for problem in problems:
        # sleep to avoid rate limiting
        sleep(5)
        problem_id = problem[0]
        language = get_desired_language(database_connector, problem_id)
        problem_header = problem[7]
        problem_content = problem[8]
        # format how we want the responses to be given to openai
        prompt = f"Using {language}, code a solution for the following prompt:\n{problem_content}\nBegin your solution with:\n{problem_header}\n"
        max_tokens = int(4096 - (len(prompt)))

        while max_tokens < 0:
            problem_content = "\n".join(problem_content.split("\n")[:-1])
            prompt = f"Using {language}, code a solution for the following prompt:\n{problem_content}\n\nBegin your solution with:\n{problem_header}\n\n"
            max_tokens = int(4096 - (len(prompt)))

        if(max_tokens > 0):
            # retrieve openai response with desired params
            response = openai.Completion.create(
                model = openai_model,
                prompt = prompt,
                temperature = 1.0,  # this is equal to "randomness", we want the ai to have full reign so set to 1
                # temperature = 0,
                max_tokens = max_tokens,   # set this to be high to get proper results
                # top_p = 0,
                top_p = 1.0,
                frequency_penalty = 0.0,
                presence_penalty = 0.0,
                # stop=["\"\"\""]
            )
            result = response['choices'][0]['text']
            if len(result) > 0:
                # need to add in the header if not present
                if problem_header not in result:
                    result = f"{problem_header}\n\n{result}"

                # save response to the dB
                database_connector.update_table(
                    table = "ChatGPT.leetcode_benchmark",
                    cols = ["openai_response"],
                    values = [result],
                    condition = f" WHERE id = {problem_id}"
                )


def submit_results(database_connector, leetcode_handler):
    # get all problems in dB with no result
    # problems = database_connector.select_from_table(
    #     table = "ChatGPT.leetcode_benchmark",
    #     col_choice = "*",
    #     col = ["openai_response", "id"],
    #     value = [None, "(SELECT problem_id FROM ChatGPT.leetcode_success)"],
    #     comparison = ["is not", "not in"],
    # )
    problems = database_connector.get_all_problems_for_submission()
    # login to leetcode
    leetcode_handler.login()
    # submit each problem and record each response
    for problem in problems[1:]:
        sleep(5)
        problem_id = problem[0]
        problem_url = problem[3]
        problem_header = problem[7]
        openai_response = problem[9]
        language = get_desired_language(database_connector, problem_id)
        try:
            result = leetcode_handler.submit_problem(language, problem_url, openai_response)
        except Exception as e:
            raise e
        database_connector.insert_into_table(
            table = "ChatGPT.leetcode_success",
            cols = ["problem_id", "succeeded", "runtime", "runtime_beats", "memory", "memory_beats", "error_type", "error_message", "total_testcases", "testcases_passed"],
            values = (
                problem_id,
                result["succeeded"],
                result["runtime"],
                result["runtime_beats"],
                result["memory"],
                result["memory_beats"],
                result["error_type"],
                result["error_message"],
                result["total_testcases"],
                result["testcases_passed"],
            ),
            ignore = True
        )


def get_desired_language(database_connector, problem_id):
    topic_tags = [tag[0] for tag in database_connector.select_from_table(
        table = "ChatGPT.leetcode_tags",
        col_choice = "topic_tag",
        col = ["problem_id"],
        value = [problem_id],
    )]
    if "shell" in topic_tags:
        return "bash"
    elif "database" in topic_tags:
        return "mysql"
    return "python3"    # default language to use
    

def process_results(database_connector, save_results=False):
    """
    This is finding the results of all the problems and percentages we are interested in.
    The function can potentially be optimized by iterating the problems once and keeping running total of the values
    instead of what we are currently doing which is individual one line iterations. Would convert from O(cn) to O(n);
    however, I think this syntax may be a bit more clear, also, this will only be ran once then have the results stored to a json.
    """
    
    results = {}
    database_connector.set_mode()
    problems = database_connector.get_all_problems()
    
    # p[5] : difficulty
    # p[10] : succeeded
    # p[15] : error type
    # p[19] : topic_tags
    
    # store overall results
    results["overall"] = {"correct": {}, "incorrect": {}}
    total = len(problems)
    
    # correct
    total_correct = len([p for p in problems if p[10]==True])
    results["overall"]["correct"]["total"] = total
    results["overall"]["correct"]["amount"] = total_correct
    results["overall"]["correct"]["percent"] = str(round(total_correct / total * 100, 2))
    # incorrect
    total_wrong = total - total_correct
    results["overall"]["incorrect"]["total"] = total
    results["overall"]["incorrect"]["amount"] = total_wrong
    results["overall"]["incorrect"]["percent"] = str(round(total_wrong / total * 100, 2))

    # store difficulty
    results["difficulty"] = {"easy": {}, "medium": {}, "hard": {}}
    # percent of easy correct
    total_easy = len([p for p in problems if p[5].lower()=="easy"])
    results["difficulty"]["easy"]["total"] = total_easy
    total_easy_correct = len([p for p in problems if p[5].lower()=="easy" and p[10]==True])
    results["difficulty"]["easy"]["amount"] = total_easy_correct
    results["difficulty"]["easy"]["percent"] = str(round(total_easy_correct / total_easy * 100, 2))
    # percent of medium correct
    total_medium = len([p for p in problems if p[5].lower()=="medium"])
    results["difficulty"]["medium"]["total"] = total_medium
    total_medium_correct = len([p for p in problems if p[5].lower()=="medium" and p[10]==True])
    results["difficulty"]["medium"]["amount"] = total_medium_correct
    results["difficulty"]["medium"]["percent"] = str(round(total_medium_correct / total_medium * 100, 2))
    # percent of hard correct
    total_hard = len([p for p in problems if p[5].lower()=="hard"])
    results["difficulty"]["hard"]["total"] = total_hard
    total_hard_correct = len([p for p in problems if p[5].lower()=="hard" and p[10]==True])
    results["difficulty"]["hard"]["amount"] = total_hard_correct
    results["difficulty"]["hard"]["percent"] = str(round(total_hard_correct / total_hard * 100, 2))
    
    # store algorithm
    results["topic"] = {"algorithm": {}, "database": {}, "shell": {}}
    # percent of algorithms correct
    total_algorithms = len([p for p in problems if "shell" not in p[19].split(",") and "database" not in p[19].split(",")])
    results["topic"]["algorithm"]["total"] = total_algorithms
    total_algorithm_correct = len([p for p in problems if "shell" not in p[19].split(",") and "database" not in p[19].split(",") and p[10]==True])
    results["topic"]["algorithm"]["amount"] = total_algorithm_correct
    results["topic"]["algorithm"]["percent"] = str(round(total_algorithm_correct / total_algorithms * 100, 2))
    # percent of database correct
    total_database = len([p for p in problems if "database" in p[19].split(",")])
    results["topic"]["database"]["total"] = total_database
    total_database_correct = len([p for p in problems if "database" in p[19].split(",") and p[10]==True])
    results["topic"]["database"]["amount"] = total_database_correct
    results["topic"]["database"]["percent"] = str(round(total_database_correct / total_database * 100, 2))
    # percent of shell correct
    total_shell = len([p for p in problems if "shell" in p[19].split(",")])
    results["topic"]["shell"]["total"] = total_shell
    total_shell_correct = len([p for p in problems if "shell" in p[19].split(",") and p[10]==True])
    results["topic"]["shell"]["amount"] = total_shell_correct
    results["topic"]["shell"]["percent"] = str(round(total_shell_correct / total_shell * 100, 2))
    
    # store break down of each algo topic tag
    results["algorithm_breakdown"] = {}
    distinct_algorithm_topic_tags = database_connector.get_distinct_algorithm_topic_tags()
    for topic in distinct_algorithm_topic_tags:
        topic = topic[0]
        results["algorithm_breakdown"][topic] = {}
        total_topic = len([p for p in problems if topic in p[19].split(",")])
        results["algorithm_breakdown"][topic]["total"] = total_topic
        total_topic_correct = len([p for p in problems if topic in p[19].split(",") and p[10]==True])
        results["algorithm_breakdown"][topic]["amount"] = total_topic_correct        
        if total_topic > 0: # locked have a few topics which may not show up for open
            results["algorithm_breakdown"][topic]["percent"] = str(round(total_topic_correct / total_topic * 100, 2))
    
    # store performance
    results["performance"] = {"runtime": {}, "memory": {}}
    # average percent of runtime beating
    average_percent_runtime_beat_list = [p[12] for p in problems if p[12]]
    average_percent_runtime_beat = sum(average_percent_runtime_beat_list) / len(average_percent_runtime_beat_list)
    results["performance"]["runtime"]["percent"] = str(round(average_percent_runtime_beat, 2))    
    # average percentage of memory beating
    average_percent_memory_beat_list = [p[14] for p in problems if p[14]]
    average_percent_memory_beat = sum(average_percent_memory_beat_list) / len(average_percent_memory_beat_list)
    results["performance"]["memory"]["percent"] = str(round(average_percent_memory_beat, 2))
    
    # store errors
    results["errors"] = {"wrong_answer": {}, "time_limit_exceeded": {}, "runtime_error": {}}
    # wrong answer, runtime error
    total_wrong_answer = len([p for p in problems if p[10]==False and p[15].lower()=="wrong answer"])
    results["errors"]["wrong_answer"]["total"] = total_wrong
    results["errors"]["wrong_answer"]["amount"] = total_wrong_answer
    results["errors"]["wrong_answer"]["percent"] = str(round(total_wrong_answer / total_wrong * 100, 2))
    # time limit exceeded
    total_time_exceeded = len([p for p in problems if p[10]==False and p[15].lower()=="time limit exceeded"])
    results["errors"]["time_limit_exceeded"]["total"] = total_wrong
    results["errors"]["time_limit_exceeded"]["amount"] = total_time_exceeded
    results["errors"]["time_limit_exceeded"]["percent"] = str(round(total_time_exceeded / total_wrong * 100, 2))
    # runtime error
    total_runtime_error = len([p for p in problems if p[10]==False and p[15].lower()=="runtime error"])
    results["errors"]["runtime_error"]["total"] = total_wrong
    results["errors"]["runtime_error"]["amount"] = total_runtime_error
    results["errors"]["runtime_error"]["percent"] = str(round(total_runtime_error / total_wrong * 100, 2))
    
    # typical runtime issue
    runtime_errors = {}
    for p in [problem for problem in problems if problem[10]==False and problem[15].lower()=="runtime error"]:
        error = re.split(':|;|\n', p[16])[0]
        if error in runtime_errors.keys():
            runtime_errors[error] += 1
        else:
            runtime_errors[error] = 1
    results["runtime_breakdown"] = {}
    for p in runtime_errors:
        # runtime_errors[p] = (runtime_errors[p], runtime_errors[p] / total_runtime_error * 100)
        error_title = p.lower().replace(" ", "_")
        results["runtime_breakdown"][error_title] = {}
        results["runtime_breakdown"][error_title]["total"] = total_runtime_error
        results["runtime_breakdown"][error_title]["amount"] = runtime_errors[p]
        results["runtime_breakdown"][error_title]["percent"] = str(round(runtime_errors[p] / total_runtime_error * 100, 2))        
    
    # store testcases passed
    results["error_breakdown"] = {"test_cases": {}}
    # average percentage of testcases passed
    test_cases_list = [p[17] for p in problems if p[17]]
    average_test_cases = sum(test_cases_list) / len(test_cases_list)
    results["error_breakdown"]["test_cases"]["total"] = str(round(average_test_cases, 2))
    test_cases_passed_list = [p[18] for p in problems if p[18]]
    average_test_cases_passed = sum(test_cases_passed_list) / len(test_cases_passed_list)
    results["error_breakdown"]["test_cases"]["amount"] = str(round(average_test_cases_passed, 2))
    results["error_breakdown"]["test_cases"]["percent"] = str(round(average_test_cases_passed / average_test_cases * 100, 2))

    json_object = json.dumps(results, indent=4)
    
    if save_results:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "assets", "results", "breakdown_results.json"), "w") as f:
            json.dump(results, f)


def save_all_results(database_connector, save_results=False):
    
    all_problems_json_object = json.dumps(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "assets", "results", "all_problems.json"),
        indent=4
    )
        
    database_connector.set_mode()
    problems = [p for p in database_connector.get_all_problems()]
    
    # convert decimal to float
    
    for i in range(len(problems)):
        problems[i] = [e for e in problems[i]]
        for j in range(len(problems[i])):
            if isinstance(problems[i][j], decimal.Decimal):
                problems[i][j] = float(problems[i][j])
        
    
    all_problems_json_object = json.dumps(problems, indent=4)
    
    if save_results:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "assets", "results", "all_problems_2.json"), "w") as f:
            json.dump(all_problems_json_object, f)


if __name__ == "__main__":
    # construct logger
    logging.basicConfig(
        filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'assets', 'logs', 'results.log'),
        filemode = "a",
        level=logging.DEBUG
    )
    logger = logging.getLogger()

    # call to main
    main()
