import { AbstractControl, ValidatorFn, ValidationErrors } from '@angular/forms'

export function matchValidator(matchTo: string): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
        if (!control.parent) return null;
        const matchingControl = control.parent.get(matchTo);
        return control.value === matchingControl?.value ? null : { matching: true };
    };
}