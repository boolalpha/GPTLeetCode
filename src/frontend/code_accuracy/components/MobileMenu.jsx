import Image from 'next/image';
import Link from 'next/Link';

import styles from '../styles/Menu.module.css'

export default function MobileMenu(props) {

    const {pages} = props;

    const toggleDropDown = () => {
        var dropdown = document.querySelector("#mobileDropDown");
        var button = document.getElementById("menuButton");
        dropdown?.classList.toggle(styles.dropDownOpen);
        if (dropdown?.classList.contains(styles.dropDownOpen)) {
            if (button != null) {
                button.innerText = "✖";
            }
        } else {
            if (button != null) {
                button.innerText = "☰";
            }
        }
    }

    return (
        <div className={styles.mobileMenuParent}>
            <div className={styles.mobileMenuContainer}>
                <Link className={styles.logo} href="./" onClick={(e) => {e.stopPropagation();}}>
                    <Image src="/GPTLeetCode-Logo.png" alt="Logo" className={styles.logo_image} height={25} width={25}/>
                    ChatGPT Leetcode
                </Link>
                <button id="menuButton" className={styles.mobileMenuButton} onClick={toggleDropDown}>
                    ☰
                </button>
            </div>
            <ul id="mobileDropDown" className={styles.mobileMenuDropDown}>
                {
                    pages.map((page) => {
                        return (
                            <li className={`${styles.mobileListItem} ${page.active ? styles.mobileActivePage : ""}`} key={page.title}>
                                <a className={styles.mobileLink} href={page.link}>{page.title}</a>
                            </li>
                        );
                    })
                }
            </ul>
        </div>
    );
}
