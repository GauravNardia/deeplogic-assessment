import { get } from "svelte/store";
import { token } from "$lib/store";

const BASE_URL = 'http://localhost:8000';

export async function apiFetch(path: string, options: RequestInit = {}) {
    const authToken = get(token);
    const res = await fetch(`${BASE_URL}${path}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
            ...options.headers,

        },
    });

    if(!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'API Error');
    }

    return res.json();
    
}