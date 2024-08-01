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
			(window.matchMedia('(prefers-color-scheme: dark)').matches && 'theme-dark'))) ||
		'theme-light'
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
		document.documentElement.style.setProperty(
			'color-scheme',
			newTheme === 'theme-dark' ? 'dark' : 'light'
		);
	}
});
