import { fetchPlus } from "../services/fetchModule";

export async function travel(form) {
    return fetchPlus({
        Url: "/travel/",
        Method: "POST",
        hasUserauth: false,
        Body: form,
    });
}


export async function next() {
    return fetchPlus({
        Url: "/next_slide",
        Method: "GET",
        hasUserauth: false,
    });
}

export async function numTravel() {
    return fetchPlus({
        Url: "/numtravels",
        Method: "GET",
        hasUserauth: false,
    });
}

export async function finish() {
    return fetchPlus({
        Url: "/finish",
        Method: "POST",
        hasUserauth: false,
    });
}