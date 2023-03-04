import React, { useState } from "react";

import DesktopMenu from "./DesktopMenu";
import MobileMenu from "./MobileMenu";
import Footer from "./Footer";

import styles from '../styles/Criteria.module.css'


export default function CriteriaPage() {
    
    function toggleCloseCategory(elem) {
        elem.children[1].classList.toggle(styles.chevron_down);
        elem.nextSibling.classList.toggle(styles.open_progress_container);
    }

    return (
        <>
            <DesktopMenu 
                pages = {[
                    {title: "Results", link: "./", active: false},
                    {title: "Criteria", link: "./criteria", active: true},
                    {title: "Problems", link: "./problems", active: false},
                    {title: "Contact", link: "./contact", active: false}
                ]}
            />
            <MobileMenu 
                pages = {[
                    {title: "Results", link: "./", active: false},
                    {title: "Criteria", link: "./criteria", active: true},
                    {title: "Problems", link: "./problems", active: false},
                    {title: "Contact", link: "./contact", active: false}
                ]}
            />
            
            <div className="pageContainer">
                <div className={styles.detail_section_container}>
                    <div className={styles.category_header_container} onClick={(e) => {toggleCloseCategory(e.target)}}>
                        <p onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}>Motivation</p>
                        <img src="/down.png" className={`${styles.chevron} ${styles.chevron_down}`} onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}/>
                    </div>
                    <div className={styles.detail_text_container}>
                        <p className={styles.basic_text}>There were two main motivations fuelling this project: one, to see how reliable ChatGPT is when giving code suggestions from english prompts, and two, to see if Leetcode problems will become an antiquated means of judging ability during job interviews if ChatGPT can answer any Leetcode problem instantly.</p>
                    </div>
                </div>
                <div className={styles.detail_section_container}>
                    <div className={styles.category_header_container} onClick={(e) => {toggleCloseCategory(e.target)}}>
                        <p onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}>Prompt</p>
                        <img src="/down.png" className={`${styles.chevron} ${styles.chevron_down}`} onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}/>
                    </div>
                    <div className={styles.detail_text_container}>
                        <p className={styles.basic_text}>
                            The exact prompt that was fed to ChatGPT is as follows:<br/>
                            "Using &lt;language&gt;, code a solution for the following prompt:<br/>
                            &lt;problem_content&gt;<br/>
                            Begin your solution with:<br/>
                            &lt;problem_header&gt;"
                        </p>
                    </div>
                </div>
                <div className={styles.detail_section_container}>
                    <div className={styles.category_header_container} onClick={(e) => {toggleCloseCategory(e.target)}}>
                        <p onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}>Model</p>
                        <img src="/down.png" className={`${styles.chevron} ${styles.chevron_down}`} onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}/>
                    </div>
                    <div className={styles.detail_text_container}>
                        <p className={styles.basic_text}>
                            It must be noted that this uses GPT-3-DaVinci-003 model as opposed to the actual ChatGPT model.
                            ChatGPT does not offer an API and it is against the terms of service to scrape ChatGPT results as it will rate limit actual users from being able to access ChatGPT.
                            That being said, GPT-3-DaVinci-003 is stated by OpenAI to be much more powerful than ChatGPT. According to <a href="https://www.ghacks.net/2022/12/30/difference-between-chatgpt-and-gpt-3/" className={styles.link}>this site</a>, 
                            "GPT-3 protocol is much larger than ChatGPT. The former has a whopping 175 billion parameters making it one of the largest and most powerful AI language processing models to date, while the latter has 20 billion parameters. 
                            This is because ChatGPT has been specifically designed to generate human-like text in the context of chatbot conversations." 
                            This means that the model that is being used, GPT-3-DaVinci-003, is likely even better to be using for code generation that ChatGPT.
                            For the sake of this project, there may be places where "ChatGPT" is used synonymously to represent GPT-3-DaVinci-003.
                        </p>
                    </div>
                </div>
                <div className={styles.detail_section_container}>
                    <div className={styles.category_header_container} onClick={(e) => {toggleCloseCategory(e.target)}}>
                        <p onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}>General Algorithm</p>
                        <img src="/down.png" className={`${styles.chevron} ${styles.chevron_down}`} onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}/>
                    </div>
                    <div className={styles.detail_text_container}>
                        <ol className={styles.algorithm_list}>
                            <li>Get all the non-premium problems from Leetcode (due to the terms of service no premium Leetcode problems were scraped)
                                <ol className={styles.algorithm_list_1}>
                                    <li>Scrape all the URLs of the available problems (51 pages with ~25 problems per page).</li>
                                    <li>Iterate the table of problems for each URL and save the problem details to the database.</li>
                                </ol>
                            </li>
                            <li>Create the prompt for each problem and save it to the database.</li>
                            <li>Get ChatGPT responses to the prompts
                                <ol className={styles.algorithm_list}>
                                    <li>Feed the prompt into the OpenAI model and save the responses to the database.</li>
                                </ol>
                            </li>
                            <li>Submit the responses to Leetcode
                                <ol className={styles.algorithm_list}>
                                    <li>Navigate to the problem page.</li>
                                    <li>Select the desire language (MySQL for database problems, Bash for shell problems, and python3 for everything else).</li>
                                    <li>Enter the response into the the problem field.</li>
                                    <li>Submit the response on Leetcode.</li>
                                    <li>Record  in the database whether the response was successful or a failure and any performance metrics (Runtime beats, Memory beats, Error type, Testcases passed).</li>
                                </ol>
                            </li>
                        </ol>
                    </div>
                </div>
                <div className={styles.detail_section_container}>
                    <div className={styles.category_header_container} onClick={(e) => {toggleCloseCategory(e.target)}}>
                        <p onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}>Manual Clean Ups</p>
                        <img src="/down.png" className={`${styles.chevron} ${styles.chevron_down}`} onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}/>
                    </div>
                    <div className={styles.detail_text_container}>
                        <p>After scanning the data a few problems returned errors that did not seem fair to blame on ChatGPT, so they were fixed and re-ran.</p>
                        <ul className={styles.unordered_list}>
                            <li>
                                The python keyword `pass` would be placed before the solution causing the true solution to be skipped (around ~10 occurrences)
                            </li>
                            <li>
                                The solution would be preceded or followed by an ill-formed docstring or a rogue ellipses [..., ''', """,```] (around ~20 occurrences)
                            </li>
                            <li>
                                Due to the way the prompt was formed, the response would sometimes double the header, so the class would be defined twice (around ~100 occurrences)
                            </li>
                            <li>
                                If the problem asked for a follow up (ex. "how could this be improved?"), ChatGPT would add a paragraph of English content at the end of the solution which would result in an error (around ~10 occurrences) 
                            </li>
                        </ul>
                        <p>Please keep in mind, some of these issues may still be present as well as others that were not detected.</p>
                    </div>
                </div>
                <div className={styles.detail_section_container}>
                    <div className={styles.category_header_container} onClick={(e) => {toggleCloseCategory(e.target)}}>
                        <p onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}>Findings</p>
                        <img src="/down.png" className={`${styles.chevron} ${styles.chevron_down}`} onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}/>
                    </div>
                    <div className={styles.detail_text_container}>
                        <ul className={styles.unordered_list}>
                            <li>The responses were far from perfect, but were, overall, very coherent and impressive.</li>
                            <li>Like a human, the responses did better on easier problems than on more difficult problems.</li>
                            <li>Quite often the responses would have a pattern that would cause an error while otherwise having a valid response (see above Manual Clean Ups).</li>
                            <li>GPT-3-DaVinci-003 actually performed better than Code-DaVinci-002 which is OpenAI's specific model for crafting code responses (keep in mind this was only noticed after manually testing ~10 problems).</li>
                            <li>GPT performed worse with database and bash problems than what was hypothesized.</li>
                            <li>GPT seemed to perform better with specific algorithms than others although it has not been investigated as to what may have been the reason.</li>
                            <li>When GPT failed it seemed to favor specific error types over others.</li>
                            <li>GPT responded to the entire set of Leetcode (non-premium) problems in around &lt;20 minutes (1984 problems) not including submission time and OpenAI api response time which were both limited by response rate-limiting.</li>
                            <li>When GPT got an answer correct, it performed specifically well in regards to runtime and memory, although both of these factors are unreliable when reported by Leetcode (ex. refresh your submission and you will get different results).</li>
                        </ul>
                    </div>
                </div>
                <Footer />
            </div>
        </>
    );
};
