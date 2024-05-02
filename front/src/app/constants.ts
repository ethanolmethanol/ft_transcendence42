// constants.ts

/////////
// API //
/////////

export const API_AUTH = 'https://localhost:8000/auth';
export const API_USER = 'https://localhost:8002/user';
export const API_GAME = 'https://localhost:8001/game';

// ERROR

export const NOT_JOINED = 1
export const INVALID_ARENA = 2
export const INVALID_CHANNEL = 3

// Game status
export const WAITING = 0
export const STARTED = 1
export const OVER = 2
export const DYING = 3
export const DEAD = 4

//////////
// GAME //
//////////

export const GAME_HEIGHT = 600;
export const GAME_WIDTH = 1000;
export const LINE_THICKNESS = 10;
export const PADDLE_HEIGHT = 100;
export const PADDLE_WIDTH = 20;
export const PADDLE_SPEED = 20;
export const PADDLE_X_OFFSET = 60;
export const BALL_RADIUS = 10;
