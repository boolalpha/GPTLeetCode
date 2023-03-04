import breakdown_results from '../public/data/breakdown_results.json';
import React, { useState } from "react";

import DesktopMenu from "./DesktopMenu";
import MobileMenu from "./MobileMenu";
import Footer from "./Footer";

import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

import styles from '../styles/Home.module.css'


export default function MainPage() {
    const front_end_label = {
        overall: "Overall Results",
        difficulty: "Breakdown by Difficulty",
        topic: "Breakdown by Topic",
        algorithm_breakdown: "Breakdown by Algorithm",
        performance: "Average Performance",
        errors: "Breakdown of Errors",
        runtime_breakdown: "Breakdown of Runtime Errors",
        error_breakdown: "Testcases Passed When Errored"
    }


    function get_color(value) {
        if (value < 25) {
            return "red";
        } else if (value < 50) {
            return "orange";
        } else if (value < 75) {
            return "yellow";
        }
        return "green";
    }


    function toggleCloseCategory(elem) {
        elem.children[1].classList.toggle(styles.chevron_down);
        elem.nextSibling.classList.toggle(styles.close_progress_container);
    }

    // render() {
    return (
        <>
            <DesktopMenu 
                pages = {[
                    {title: "Results", link: "./", active: true},
                    {title: "Criteria", link: "./criteria", active: false},
                    {title: "Problems", link: "./problems", active: false},
                    {title: "Contact", link: "./contact", active: false}
                ]}
            />
            <MobileMenu 
                pages = {[
                    {title: "Results", link: "./", active: true},
                    {title: "Criteria", link: "./criteria", active: false},
                    {title: "Problems", link: "./problems", active: false},
                    {title: "Contact", link: "./contact", active: false}
                ]}
            />
            
            <div className="pageContainer">
                <p className={styles.opening_header}>The results of OpenAI's ChatGPT ran against every (non-premium) Leetcode problem.</p>
                {Object.keys(breakdown_results).map((category) => (
                    <div className={styles.category_container} key={category}>
                        <div className={styles.category_header_container} onClick={(e) => {toggleCloseCategory(e.target)}}>
                            <p onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}>{front_end_label[category]}</p>
                            <img src="/down.png" className={`${styles.chevron} ${category == "algorithm_breakdown" && styles.chevron_down}`} onClick={(e) => {e.stopPropagation(); toggleCloseCategory(e.target.parentNode)}}/>
                        </div>
                        <div className={`${styles.progress_container} ${(category == "algorithm_breakdown" || category == "runtime_breakdown") && styles.close_progress_container}`}>
                            {Object.keys(breakdown_results[category]).map((result) => (
                                <div className={styles.result_container} key={result}>
                                    <p className={styles.result_title}>
                                        {result.replace("_", " ").toLowerCase()
                                        .split(' ')
                                        .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
                                        .join(' ')}
                                    </p>
                                    <div className={styles.progressbar_wrapper}>
                                        <CircularProgressbar
                                            value={
                                                breakdown_results[category][result]["percent"]}
                                            text={`${
                                                breakdown_results[category][result]["percent"]}%`}
                                            styles={{
                                                trail: {
                                                    // Trail color
                                                    // stroke: get_color(breakdown_results[category][result]["percent"]),
                                                },
                                                path: {
                                                    // Path color
                                                    stroke: get_color(breakdown_results[category][result]["percent"]),
                                                    // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                                                    strokeLinecap: 'round',
                                                }
                                            }} />
                                    </div>
                                    { 
                                        breakdown_results[category][result]["total"] && 
                                        <p className={styles.result_breakdown}>
                                            {
                                                breakdown_results[category][result]["amount"]
                                            }
                                            /
                                            {
                                                breakdown_results[category][result]["total"]
                                            }
                                        </p>
                                    }
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
                <Footer />
            </div>
        </>
    );
};
