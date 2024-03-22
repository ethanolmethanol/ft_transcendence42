import { AbstractControl, ValidatorFn, ValidationErrors } from '@angular/forms'

export function matchValidator(matchTo: string, reverse: boolean = false): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
        const parent = control?.parent;
        const controlToMatch = parent?.get(matchTo);

        if (!control.parent) return null;

        if (reverse && controlToMatch) {
            controlToMatch.updateValueAndValidity();
            return null;
        }
        if (!parent || !controlToMatch) {
            return null;
        }
        const isMatch = control.value === controlToMatch.value;
        return isMatch ? null : { matching: true };
    };
}
