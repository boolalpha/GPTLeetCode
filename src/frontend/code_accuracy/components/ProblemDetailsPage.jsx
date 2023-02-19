import all_problems from '../public/data/all_problems.json';
import React, { useState, useEffect } from "react";
import Link from 'next/link';

import Editor from "@monaco-editor/react";

import DesktopMenu from "./DesktopMenu";
import MobileMenu from "./MobileMenu";
import Footer from "./Footer";

import styles from '../styles/ProblemDetails.module.css'


export default function ProblemsDetailsPage() {
    const [valid_page, set_valid_page] = useState(false);
    const [invalid_message, set_invalid_message] = useState("")
    const [problem_number, set_problem_number] = useState("");
    const [problem_title, set_problem_title] = useState("");
    const [problem_link, set_problem_link] = useState("");
    const [topics, set_topics] = useState("");
    const [difficulty, set_difficulty] = useState("");
    const [acceptance, set_acceptance] = useState("");
    const [problem_content, set_problem_content] = useState("");
    const [response, set_response] = useState("");
    const [success, set_success] = useState("");
    const [runtime, set_runtime] = useState("");
    const [runtime_beats, set_runtime_beats] = useState("");
    const [memory, set_memory] = useState("");
    const [memory_beats, set_memory_beats] = useState("");
    const [error_type, set_error_type] = useState("");
    const [error_message, set_error_message] = useState("");
    const [testcases_passed, set_testcases_passed] = useState("");
    const [total_testcases, set_total_testcases] = useState("");

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const problem_number_parameter = +urlParams.get("problem_number");
        if (problem_number_parameter) {
            var number_in_range = false;
            var problem_index = null;
            for (var i = 0; i < all_problems.length; i++) {
                if (all_problems[i].problem_number === problem_number_parameter) {
                    number_in_range = true;
                    problem_index = i;
                    break;
                }
            }

            if (number_in_range) {
                // get the problem content
                const problem = all_problems[problem_index];
                // set all the problem content
                set_problem_number(problem.problem_number);
                set_problem_title(problem.title);
                set_problem_link(problem.problem_url);
                set_topics(problem.topics);
                set_difficulty(problem.difficulty);
                set_acceptance(problem.acceptance);
                set_problem_content(problem.problem_content);
                set_response(problem.openai_response);
                
                if (problem.succeeded) {
                    set_runtime(problem.runtime);
                    set_runtime_beats(problem.runtime_beats);
                    set_memory(problem.memory);
                    set_memory_beats(problem.memory_beats);
                    set_success(true);
                } else {
                    set_error_type(problem.error_type);
                    set_error_message(problem.error_message);
                    set_testcases_passed(problem.testcases_passed);
                    set_total_testcases(problem.total_testcases);
                    set_success(false);
                }

                // show the page
                set_valid_page(true);
            } else {
                // set the message
                set_invalid_message("The problem number provided is out of bounds");
                // hide the valid page, show the invalid page
                set_valid_page(false);
            }
        } else {
            // set the message
            set_invalid_message("The problem number provided is invalid");
            // hide the valid page, show the invalid page
            set_valid_page(false);
        }
        
    });

    var split_topics = topics.split(',');
    
    // const [color, setColor] = useState("");
    
    // if (difficulty.toLowerCase() === "medium") {
    //     setColor("orange");
    // } else if (difficulty.toLowerCase() === "hard") {
    //     setColor("red");
    // }

    return (
        <>
            <DesktopMenu 
                pages = {[
                    {title: "Results", link: "./", active: false},
                    {title: "Criteria", link: "./criteria", active: false},
                    {title: "Problems", link: "./problems", active: false},
                    {title: "Contact", link: "./contact", active: false}
                ]}
            />
            <MobileMenu 
                pages = {[
                    {title: "Results", link: "./", active: false},
                    {title: "Criteria", link: "./criteria", active: false},
                    {title: "Problems", link: "./problems", active: false},
                    {title: "Contact", link: "./contact", active: false}
                ]}
            />
            
            
            <div className="pageContainer">
                <div className={`${styles.pageHolder} ${valid_page === true && styles.hide}`}>
                    <p className={styles.invalid_message}>{invalid_message}</p>
                    <Footer />
                </div>
                <div className={`${styles.pageHolder} ${valid_page === false && styles.hide}`}>
                    <div className={styles.header_container}>
                        <div className={styles.main_title_container}>
                            <div className={styles.title_container}>
                                <p>{problem_number}.</p>
                                <p>{problem_title}</p>
                            </div>
                            <Link className={styles.source_link} href={problem_link}>Source</Link>
                        </div>
                        <div className={styles.topics_container}>
                            {
                                split_topics.map((topic) => 
                                    <div className={styles.topic} key={topic}>
                                        {topic}
                                    </div>
                                )
                            }
                        </div>
                        <div className={styles.difficulty_container}>
                            <p className={styles.color_container + `
                                ${
                                    difficulty.toLowerCase() === "hard" ? styles.red : 
                                    difficulty.toLowerCase() === "medium" ? styles.orange :
                                    styles.green
                                }
                            `}>{difficulty}</p>
                            <p className={styles.color_container + `
                                ${
                                    +acceptance >= 66.66 ? styles.red :
                                    +acceptance >= 33.33 ? styles.orange :
                                    styles.green
                                }
                            `}>{acceptance}% acceptance</p>
                        </div>
                    </div>
                    <div className={styles.results_container}>
                        <p className={styles.category_title}>Results:</p>
                        <p className={styles.success_message}>
                            ChatGPT got this problem <span className={styles.highlight_text + " " + `${
                                success ? styles.success_message_correct : styles.success_message_incorrect
                            }`}                            
                            >{success ? "correct" : "wrong"}
                            </span>
                        </p>
                        <div className={styles.results_message_container + " " + `${!success ? styles.hide : undefined}`}>
                            <p>
                                Runtime:
                                    <span className={styles.highlight_text + " " + `${
                                        +runtime_beats >= 50 ? styles.good_result : styles.bad_result
                                    }`}> {runtime} ms </span>
                                beats 
                                    <span className={styles.highlight_text + " " + `${
                                        +runtime_beats >= 50 ? styles.good_result : styles.bad_result
                                    }`}> {runtime_beats}% </span>
                                of submissions
                            </p>
                            <p>
                                Memory:
                                    <span className={styles.highlight_text + " " + `${
                                        +memory_beats >= 50 ? styles.good_result : styles.bad_result
                                    }`}> {memory} mb </span>
                                beats: 
                                    <span className={styles.highlight_text + " " + `${
                                        +memory_beats >= 50 ? styles.good_result : styles.bad_result
                                    }`}> {memory_beats}% </span>
                                of submissions
                            </p>
                        </div>
                        <div className={styles.results_message_container + " " + `${success ? styles.hide : undefined}`}>
                            <p>Error type: 
                                <span className={styles.error_testcases}> {error_type}</span>
                            </p>
                            <div>
                                <p>Testcases passed: 
                                    <span className={styles.error_testcases}> {testcases_passed}</span>
                                </p>
                                <p>Total testcases: 
                                    <span className={styles.error_testcases}> {total_testcases}</span>
                                </p>
                            </div>
                        </div>
                    </div>
                    <div className={styles.content_container}>
                        <div className={styles.prompt_container}>
                            <p className={styles.category_title}>Problem Content:</p>
                            <p className={styles.problem_content}>{problem_content}</p>
                        </div>
                        <div className={styles.response_container}>
                            <p className={styles.category_title}>ChatGPT Response:</p>
                            <Editor
                                className={styles.response}
                                height="75vh"
                                defaultLanguage={
                                    split_topics.includes("database") ? "mysql" :
                                    split_topics.includes("shell") ? "shell" :
                                    "python"
                                }
                                defaultValue={response}
                                options={{readOnly: true}}
                                theme="vs-dark"
                            />
                        </div>
                    </div>
                    <Footer />
                </div>
            </div>
        </>
    );
};