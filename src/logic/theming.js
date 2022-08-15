import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined';

export const themes = [
	{
		id: 'theme-light',
		name: 'Light theme',
		icon: 'light_mode',
	},
	{
		id: 'theme-dark',
		name: 'Dark theme',
		icon: 'dark_mode',
	},
];

export const theme = writable(
	(isBrowser &&
		(window.localStorage.getItem('theme') ||
			(window.matchMedia('(prefers-color-scheme: light)').matches && 'theme-light'))) ||
		'theme-dark'
);

theme.subscribe((newTheme) => {
	if (isBrowser) {
		if (!newTheme.startsWith('theme-')) newTheme = 'theme-' + newTheme;

		window.localStorage.setItem('theme', newTheme);

		document.body.classList.add(newTheme);
		document.body.classList.forEach((className) => {
			if (className !== newTheme && className.startsWith('theme-'))
				document.body.classList.remove(className);
		});
	}
});
