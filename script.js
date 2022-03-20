/**
 * Template variables that have a prefix of '$' will be replaced with real values at compile time.
 */

/**
 * @type {string[]} - array of img paths
 */
const paths = $paths;

class Visibility {
  /**
   * true if visible, false otherwise
   * @type {boolean}
   */
  _value

  /**
   * Create an instance whose visibility is set to true
   */
  static createVisible() {
    return new Visibility(true);
  }

  /**
   * @param {boolean} value
   */
  constructor(value) {
    this._value = value;
  }

  /**
   * Set visibility
   * @param {boolean} value
   */
  set(value) {
    this._value = value;
  }

  /**
   * return a value used for data attribute in an HTML element
   * @returns {string}
   */
  toDataAttr() {
    return this._value ? "1" : "0"
  }
}

/**
 * @type {Map<string, Visibility>} - the key is an img path and the boolean value indicates whether the img should be visible or not.
 */
const filterMap = new Map(paths.map(path => [path, Visibility.createVisible()]));

/**
 * @type {Map<string, HTMLElement>} - the key is an img path and the value is an HTML element that corresponds with the img path.
 */
const itemElemMap = new Map(
  Array.from(document.getElementsByClassName('item'))
    .map(elem => [elem.dataset.path, elem])
);

/**
 * Show all the images.
 * @param {Map<string, Visibility>} filterMap 
 * @returns {void}
 */
function showAll(filterMap) {
  for (const path of filterMap.keys()) {
    filterMap.get(path).set(true);
  }
}

/**
 * Sanitize the user input
 * @param {string} input
 * @returns {string}
 */
function sanitize(input) {
  return input.trim();
}

/**
 * Filter the images by a provided keyword.
 * @param {string} keyword
 * @param {Map<string, Visibility>} filterMap 
 * @returns {void}
 */
function filter(keyword, filterMap) {
  const sanitizedKeyword = keyword.trim();

  if (sanitizedKeyword.length) {
    for (const path of filterMap.keys()) {
      filterMap.get(path).set(path.includes(sanitizedKeyword));
    }
  } else {
    showAll(filterMap);
  }
}

/**
 * Render the visibility of the images according to filterMap.
 * @param {Map<string, Visibility>} filterMap 
 * @param {Map<string, HTMLElement>} itemElemMap
 * @returns {void}
 */
function render(filterMap, itemElemMap) {
  for (const [path, visibility] of filterMap) {
    itemElemMap.get(path).dataset.visible = visibility.toDataAttr();
  }
}

class Timer {
  /**
   * Singleton instance
   * @type {?Timer}
   */
  _instance = null;

  /**
   * The time at which the timer has started.
   * @type {Date}
   */
  _startedAt = null;

  /**
   * The duration of time to wait in millisec before firing the callback.
   * @type {number}
   */
  _WAIT_FOR_MS = 500;

  /**
   * The interval of time after which whether to fire the callback will be checked.
   * @type {number}
   */
  _CLOCK_INTERVAL = 100;

  /**
   * A function to be called after a certain amount of time, specified in _WAIT_FOR_MS, has passed.
   * @type {?Function}
   */
  _callback = null;

  /**
   * Return the singleton instance.
   * @returns {Timer}
   */
  static getInstance() {
    if (!Timer._instance) Timer._instance = new Timer();

    return Timer._instance;
  }
  
  /**
   * Don't call the constructor from outside. Call 'getInstance' static method to obtain the singleton instance instead.
   */
  constructor() {
    setInterval(() => {
      this._fireCallbackIfReady();
    }, this._CLOCK_INTERVAL);
  }

  /**
   * Register a callback and start the timer. If there is already a callback registered, the callback will be overwritten by the new one and the timer will restart.
   * @param {Function} callback
   */
  start(callback) {
    this._startedAt = new Date(); // need to reset the time BEFORE registering the callback to prevent the callback from being immediately called after registered
    this._callback = callback;
  }

  /**
   * Fire the registered callback if the conditions are met. Conditions are:
   * - the duration of time specified in _WAIT_FOR_MS has passed.
   * - a callback function is registered.
   * 
   * Deregster the callback after it's called.
   * @returns {void}
   */
  _fireCallbackIfReady() {
    if (this._hasWaitedEnough() && this._callback) {
      this._callback();
      this._callback = null;
    }
  }

  /**
   * @returns {boolean}
   */
  _hasWaitedEnough() {
    return new Date() - this._startedAt >= this._WAIT_FOR_MS;
  }
}

const timer = Timer.getInstance();

const input = document.getElementById('filter-input');

input.addEventListener('input', (e) => {
  timer.start(() => {
    filter(sanitize(e.target.value), filterMap);
    render(filterMap, itemElemMap);
  });
});

const LIGHT_MODE_DATA_ATTR = "light";
const lightModeBtn = document.getElementById('light-mode-btn');
lightModeBtn.addEventListener('click', (e) => document.getRootNode().documentElement.dataset.mode = LIGHT_MODE_DATA_ATTR);

const DARK_MODE_DATA_ATTR = "dark";
const darkModeBtn = document.getElementById('dark-mode-btn');
darkModeBtn.addEventListener('click', (e) => document.getRootNode().documentElement.dataset.mode = DARK_MODE_DATA_ATTR);
