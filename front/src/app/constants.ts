// constants.ts

////////////////
// COMPONENTS //
////////////////

/////////
// API //
/////////

import { environment } from "../environments/environment";

export const API_AUTH = `https://${environment.servIP}:8000/auth`;
export const API_USER = `https://${environment.servIP}:8002/user`;
export const API_GAME = `https://${environment.servIP}:8001/game`;
export const API_GAME_SOCKET = `wss://${environment.servIP}:8001`;

// TIMEZONE

export const TIME_ZONE = 'Europe/Paris';
export const LOCALE = 'en-US';

// INTERFACES

export const CHANNEL_ID_LENGTH = 10;

// TIME

export const JOIN_GAME_RETRY_DELAY_MS = 2000;

// ERROR

export const NOT_JOINED = 1
export const INVALID_ARENA = 2
export const INVALID_CHANNEL = 3
export const NOT_ENTERED = 4
export const GIVEN_UP = 5

// Game status
export const CREATED = 0
export const WAITING = 1
export const READY_TO_START = 2
export const STARTED = 3
export const OVER = 4
export const DYING = 5
export const DEAD = 6

// Game History

export const GAME_HISTORY_COUNT_REQUEST = 4

//////////
// GAME //
//////////

export const GAME_HEIGHT = 800;
export const GAME_WIDTH = 1200;
export const LINE_THICKNESS = 10;
export const PADDLE_HEIGHT = 100;
export const PADDLE_WIDTH = 20;
export const PADDLE_SPEED = 20;
export const PADDLE_X_OFFSET = 60;
export const BALL_RADIUS = 10;

// Game options
export const BALL_SPEED = 0
export const PADDLE_SIZE = 1
export const OPPONENTS_LOCAL = 2
export const OPPONENTS_ONLINE = 3
export const AI_OPPONENTS_LOCAL = 4
export const AI_OPPONENTS_ONLINE = 5
export const IS_PRIVATE = 6

export const OPTIONS_LABELS = ['Ball Speed', 'Paddle Size', 'Human Opponents', 'Online Opponents', 'AI Opponents', 'AI Opponents', 'Visibility']

export const BALL_SPEED_OPTIONS = ['snail', 'deer', 'lion', 'hawk', 'jet']
export const PADDLE_SIZE_OPTIONS = ['tiny', 'small', 'medium', 'large', 'jumbo']
export const OPPONENTS_LOCAL_OPTIONS = ['0', '1']
export const OPPONENTS_ONLINE_OPTIONS = ['1', '2', '3']
export const AI_OPPONENTS_LOCAL_OPTIONS = ['0', '1', '2', '3']
export const AI_OPPONENTS_ONLINE_OPTIONS = ['0', '1', '2']
export const IS_PRIVATE_OPTIONS = ['public', 'private']
export const OPTIONS = [BALL_SPEED_OPTIONS, PADDLE_SIZE_OPTIONS, OPPONENTS_LOCAL_OPTIONS, OPPONENTS_ONLINE_OPTIONS, AI_OPPONENTS_LOCAL_OPTIONS, AI_OPPONENTS_ONLINE_OPTIONS, IS_PRIVATE_OPTIONS]

export const BALL_SPEED_DEFAULT = 2
export const PADDLE_SIZE_DEFAULT = 2
export const NUMBER_PLAYERS_DEFAULT = 1
export const HUMAN_OPPONENTS_DEFAULT = 1
export const AI_OPPONENTS_DEFAULT = 0
export const IS_PRIVATE_DEFAULT = 1
export const DEFAULT_SETTINGS = [BALL_SPEED_DEFAULT, PADDLE_SIZE_DEFAULT, NUMBER_PLAYERS_DEFAULT, HUMAN_OPPONENTS_DEFAULT, AI_OPPONENTS_DEFAULT, AI_OPPONENTS_DEFAULT, IS_PRIVATE_DEFAULT]
export const MAX_OPPONENTS = 3

export const BALL_COLOR = 0
export const PADDLE_COLOR = 1
export const BACKGROUND_COLOR1 = 2
export const BACKGROUND_COLOR2 = 3
export const LINE_COLOR = 4
export const SCORE_COLOR = 5
export const DEFAULT_COLORS = ['#ffffff', '#ffffff', '#000000', '#000000', '#aaaaaa', '#dcdcdc80']

export const DEFAULT_TIME_PLAYED = {local: 0, remote: 0, total: 0}
export const DEFAULT_GAME_COUNTER = {local: 0, remote: 0, total: 0}
export const DEFAULT_WIN_DICT = {win: 0, loss: 0, tie: 0, total: 0}

export const MINIO_API: string = `https://${environment.servIP}:9000`
export const AVATARS_BUCKET: string = "avatars"
export const DEFAULT_AVATAR_URL: string = `${MINIO_API}/${AVATARS_BUCKET}/default_avatar.jpg`

export const ACCOUNT: number = 0;
export const GAME: number = 1;
export const RULES: number = 2;
export const FRIENDS: number = 3;
