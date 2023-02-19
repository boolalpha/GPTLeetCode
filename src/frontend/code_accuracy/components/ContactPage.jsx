import DesktopMenu from "./DesktopMenu";
import MobileMenu from "./MobileMenu";

import Link from 'next/link';

import styles from '../styles/Contact.module.css';


// class MainPage extends React.Component <{}> {
export default function MainPage() {
    return (
        <>
            <DesktopMenu 
                pages = {[
                    {title: "Results", link: "./", active: false},
                    {title: "Criteria", link: "./criteria", active: false},
                    {title: "Problems", link: "./problems", active: false},
                    {title: "Contact", link: "./contact", active: true}
                ]}
            />
            <MobileMenu 
                pages = {[
                    {title: "Results", link: "./", active: false},
                    {title: "Criteria", link: "./criteria", active: false},
                    {title: "Problems", link: "./problems", active: false},
                    {title: "Contact", link: "./contact", active: true}
                ]}
            />
            
            <div className={`pageContainer + ${styles.contact_page}`}>
                <Link href="https://boolalpha.com" className={styles.contact_item}>Built By BoolAlpha</Link>
                <Link href="mailto:consult@boolalpha.com" className={styles.contact_item}>consult@boolalpha.com</Link>
                <Link href="https://github.com/BoolAlpha" className={styles.contact_item}>GitHub Repo</Link>
                <Link href="https://leetcode.com/chatgptbot/" className={styles.contact_item}>Leetcode Profile</Link>
            </div>
        </>
    );
};
