import { AbstractControl, ValidatorFn } from '@angular/forms'

export function emailValidator(): ValidatorFn {
    return (control: AbstractControl): {[key: string]: any} | null => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const valid = emailRegex.test(control.value);
        return valid ? null : {'invalidEmail': {value: control.value}};
    };
}