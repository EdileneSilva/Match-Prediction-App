const gsapMock = {
  context: jest.fn(() => ({ revert: jest.fn() })),
  fromTo: jest.fn(),
  from: jest.fn(),
  to: jest.fn(),
  set: jest.fn(),
  killTweensOf: jest.fn(),
  timeline: jest.fn(() => ({
    to: jest.fn(),
    from: jest.fn(),
    fromTo: jest.fn(),
    set: jest.fn(),
    add: jest.fn(),
    play: jest.fn(),
    pause: jest.fn(),
    seek: jest.fn(),
    progress: jest.fn(),
    duration: jest.fn(),
    time: jest.fn(),
    eventCallback: jest.fn(),
    repeat: jest.fn(),
    yoyo: jest.fn(),
    repeatDelay: jest.fn(),
    delay: jest.fn()
  })),
  quickTo: jest.fn(() => jest.fn()),
  registerPlugin: jest.fn(),
  defaults: {},
  utils: {
    snap: jest.fn(),
    random: jest.fn(),
    distribute: jest.fn()
  }
}

// Export both default and named exports to handle different import styles
export default gsapMock
export { gsapMock as gsap }