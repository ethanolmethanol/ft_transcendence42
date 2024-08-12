import {ErrorResponse} from "./error-response.interface";

export interface VariableMapping {
  [key: string]: (value: any) => void;
}

export interface ErrorMapping {
  [key: number]: (value: ErrorResponse) => void;
}
