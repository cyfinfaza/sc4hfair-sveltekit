import { year as shYear } from 'data/shClues.json';

const SCAVENGER_HUNT_PREFIX = `sh_${shYear}_`;
export const SCAVENGER_HUNT_CODE = SCAVENGER_HUNT_PREFIX + 'code';
export const SCAVENGER_HUNT_HINTS = SCAVENGER_HUNT_PREFIX + 'hints';

/** @type {string} */
// @ts-expect-error
export const BRANCH = __BRANCH__;
/** @type {string} */
// @ts-expect-error
export const BUILD_TIME = __BUILD_TIME__;
/** @type {string} */
// @ts-expect-error
export const BUILD_LOCATION = __BUILD_LOCATION__;
/** @type {string} */
// @ts-expect-error
export const WEBPUSH_API_PREFIX = __WEBPUSH_API_PREFIX__;
