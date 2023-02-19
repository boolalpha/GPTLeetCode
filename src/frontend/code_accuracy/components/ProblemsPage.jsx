import all_problems from '../public/data/all_problems.json';
import React, { useCallback, useState } from "react";
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import { faChevronDown } from '@fortawesome/free-solid-svg-icons'

// works
import { DataGrid } from '@mui/x-data-grid';

import DesktopMenu from "./DesktopMenu";
import MobileMenu from "./MobileMenu";
import Footer from "./Footer";

import styles from '../styles/Problems.module.css'

export default function ProblemsPage() {

    const [ filter, set_filter ] = useState([]);

    // mui
    const columns = [
        { 
            field: 'id', 
            headerName: 'Problem Number',
            flex: 1,
            align: 'center',
            headerAlign: 'center',
            headerClassName: "super-app-theme--header"

        },
        {
            field: 'title',
            headerName: 'Title',
            flex: 1,
            align: 'center',
            headerAlign: 'center',
      
        },
        {
            field: 'difficulty',
            headerName: "Difficulty",
            flex: 1,
            align: 'center',
            headerAlign: 'center',
            renderCell: (mui_details) => {
                return (
                    <p className={`
                        ${
                            mui_details.row.difficulty.toLowerCase() === "easy" ? styles.green :
                            mui_details.row.difficulty.toLowerCase() === "medium" ? styles.orange : 
                            styles.red
                        }
                    `}>
                        {mui_details.row.difficulty}
                    </p>
                );
            }
        },
        {
            field: 'succeeded',
            headerName: "Succeeded",
            flex: 1,
            align: 'center',
            headerAlign: 'center',
            renderCell: (mui_details) => {
                return (
                    <p className={`
                        ${
                            mui_details.row.succeeded.toLowerCase() === "true" ? styles.green : styles.red
                        }
                    `}>
                        {mui_details.row.succeeded}
                    </p>
                );
            }
        },
        {
            field: "topics",
            headerName: "Topic Tags",
            flex: 1,
            align: 'center',
            headerAlign: 'center',
            renderCell: (mui_details) => {
                const split_topics = mui_details.row.topics.split(',');
                return (
                    <div className={styles.topics_container}>
                        {split_topics.map((topic) =>
                            <button className={styles.topic_button} onClick={(event) => {
                                event.stopPropagation();
                                set_filter([
                                    {
                                        columnField: "topics",
                                        operatorValue: "contains",
                                        value: topic,
                                    }
                                ])
                            }} key={topic}>
                                {topic}
                            </button>
                        )}
                    </div>
                );
            }
        }
      
    ];

    const [sort_model, set_sort_model] = useState([
        {
            field: 'id',
            sort: 'asc'
        }
    ]);

    let rows = [];

    for (var i = 0; i < all_problems.length; i++) {        
        // mui
        rows.push({
            id: all_problems[i].problem_number,
            title: all_problems[i].title,
            difficulty: all_problems[i].difficulty,
            succeeded: all_problems[i].succeeded ? "True" : "False",
            topics: all_problems[i].topics
        });
    }

    const on_row_click = useCallback((rowProps, event) => {
        // mui
        window.location.href = "./problemdetails?problem_number=" + rowProps.id;
    }, []);

    return (
        <>
            <DesktopMenu 
                pages = {[
                    {title: "Results", link: "./", active: false},
                    {title: "Criteria", link: "./criteria", active: false},
                    {title: "Problems", link: "./problems", active: true},
                    {title: "Contact", link: "./contact", active: false}
                ]}
            />
            <MobileMenu 
                pages = {[
                    {title: "Results", link: "./", active: false},
                    {title: "Criteria", link: "./criteria", active: false},
                    {title: "Problems", link: "./problems", active: true},
                    {title: "Contact", link: "./contact", active: false}
                ]}
            />
 
            <div className="pageContainer">
                <DataGrid 
                    sx={{
                        // m: 4,
                        p: 2,
                        border: 0,
                        cursor: 'pointer',
                        color: "white",
                        "& .MuiDataGrid-row:hover": {
                            backgroundColor: "rgba(218, 165, 32, 0.25)"
                        },
                        "& .MuiTablePagination-root, \
                        & .MuiSvgIcon-root, \
                        & .MuiButtonBase-root, \
                        & .MuiIconButton-root": {
                            color: "white"
                        }
                    }}
                    rows={rows}
                    columns={columns}
                    onRowClick={on_row_click}
                    sortModel={sort_model}
                    onSortModelChange={(new_sort_model) => {
                        set_sort_model(new_sort_model);
                    }}
                    getRowClassName={(params) =>
                        params.indexRelativeToCurrentPage % 2 === 0 ? styles.even_row : styles.odd_row
                    }
                    className={styles.data_grid}
                    filterModel={{
                        items: filter
                    }}
                    getRowHeight={() => 'auto'}
                    // components={{Footer: CustomFooter}}
                />
                <Footer></Footer>
            </div>
        </>
    );
};
