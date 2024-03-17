// Code adapted from https://github.com/consultingninja/svelteTemplateProject/blob/main/src/utils/linkUtil.js

import svelteLogo from '../assets/svelte.svg';

export const linkUtil = {
    logo: true,
    logoSrc:svelteLogo,
    logoLink:true,
    linkUrl: '#/',
    optionalLinkText: 'velte',
    copyrightNotice: `ConsultingNinja  © 2022`,
    altText: 'Logo',
    links:[
        {url:'#/',
        displayInNav: true,
        displayInFooter: true,
        linkText: 'Home'
    },
    {url:'#/about',
    displayInNav: true,
    displayInFooter: true,
    linkText: 'Time Analysis'
    },
    {url:'#/contact',
    displayInNav: true,
    displayInFooter: true,
    linkText: 'Deep Dive Analysis'
    },
    {url:'#/help',
    displayInNav: true,
    displayInFooter: true,
    linkText: 'Help'
    },
    {url:'#/notfound',
    displayInNav: false,
    displayInFooter: false,
    linkText: ''
    },
    ]
}