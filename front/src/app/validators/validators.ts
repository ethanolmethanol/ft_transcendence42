import { AbstractControl, ValidatorFn, Validators } from '@angular/forms';
import validationRules from '../../../shared/validation-rules.json';

export function usernameValidator(): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any } | null => {
    const valid = new RegExp(validationRules.username.pattern).test(control.value);
    return valid ? null : { 'invalidUsername': { value: control.value } };
  };
}

export function emailValidator(): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any } | null => {
    const valid = new RegExp(validationRules.email.pattern).test(control.value);
    return valid ? null : { 'invalidEmail': { value: control.value } };
  };
}

export function passwordValidator(): ValidatorFn {
  return Validators.minLength(validationRules.password.minLength);
}
