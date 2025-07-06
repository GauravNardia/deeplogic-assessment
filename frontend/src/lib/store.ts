import { writable } from 'svelte/store';

let initialToken = '';
let initialRole = '';

if (typeof localStorage !== 'undefined') {
  initialToken = localStorage.getItem('token') || '';
  initialRole = localStorage.getItem('role') || '';
}

export const token = writable<string>(initialToken);
export const userRole = writable<string>(initialRole);

if (typeof window !== 'undefined') {
  token.subscribe((value) => {
    if (value) {
      localStorage.setItem('token', value);
    } else {
      localStorage.removeItem('token');
    }
  });

    userRole.subscribe((value) => {
    if (value) {
      localStorage.setItem('role', value);
    } else {
      localStorage.removeItem('role');
    }
  });

}
