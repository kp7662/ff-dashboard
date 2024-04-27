// The following code is adapted from: https://github.com/consultingninja/svelteTemplateProject/blob/main/src/url.js

import { derived,writable } from "svelte/store";

export function createUrlStore(Url){
    if(typeof window === 'undefined'){
        const{subscribe} = writable(Url);
        return{subscribe}
    }

    const href = writable(window.location.href);

    const originalPushState = history.pushState
    const originalReplaceState = history.replaceState

    const updateHref = () => href.set(window.location.href)

    history.pushState = function (){
        originalPushState.apply(this,arguments)
        updateHref()
    }

    history.replaceState = function (){
        originalReplaceState.apply(this,arguments)
        updateHref()
    }

    window.addEventListener('popstate',updateHref)
    window.addEventListener('hashchange',updateHref)

    return{
        subscribe: derived(href, $href => {
            try {
                return new URL($href);
            } catch (error) {
                console.error("Error creating URL object:", error);
                return null; // or some safe fallback value
            }
        }).subscribe
    }


}

export default createUrlStore()