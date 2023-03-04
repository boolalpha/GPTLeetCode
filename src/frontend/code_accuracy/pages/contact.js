import ContactPage from '../components/ContactPage';

import Head from 'next/head'

export default function Home() {
    var columns = [
        { key: 'problem_number', name: 'Problem Number', sortable: true, sortDescendingFirst: true }
    ];
    return (
        <>
            <Head>
                <title>ChatGPT Leetcode</title>
                <meta name="description" content="Generated by create next app" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <ContactPage />
        </>
    )
}
