import Link from 'next/link';

import styles from '../styles/Footer.module.css';


export default function DesktopMenu() {

    return (
        <div className={styles.footer_container}>
            <Link href="https://github.com/boolalpha/GPTLeetCode" className={styles.footer_item}>Built By BoolAlpha</Link>
            <div className={styles.footer_border}/>
            <Link href="https://github.com/boolalpha/GPTLeetCode" className={styles.footer_item}>GitHub Repo</Link>
            <div className={styles.footer_border}/>
            <Link href="https://leetcode.com/chatgptbot/" className={styles.footer_item}>Leetcode Profile</Link>
        </div>
    );
}
