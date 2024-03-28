import { SignUpComponent } from './sign-up.component';
import {AuthService} from "../../services/auth/auth.service";
import {FormBuilder} from "@angular/forms";
import {Router} from "@angular/router";
import {of} from "rxjs";

describe('SignUpComponent', () => {
  let component: SignUpComponent;
  let formBuilder: FormBuilder;
  let authServiceMock: jasmine.SpyObj<AuthService>;
  let routerMock: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    authServiceMock = jasmine.createSpyObj('AuthService', ['signUp']);
    routerMock = jasmine.createSpyObj('Router', ['navigate']);
    formBuilder = new FormBuilder();
    component = new SignUpComponent(formBuilder, authServiceMock, routerMock);
    const mockSignUpResponse = { };
    authServiceMock.signUp.and.returnValue(of(mockSignUpResponse));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize form with empty fields', () => {
    component.ngOnInit();
    expect(component.signupForm.value).toEqual({ username: '', email: '', password: '', c_password: '', updateOn: 'blur' });
  });

  it('should call onSubmit method', () => {
    spyOn(component, 'onSubmit');
    component.onSubmit();
    expect(component.onSubmit).toHaveBeenCalled();
  });

  it('should not submit if form is invalid', () => {
    component.ngOnInit();
    component.onSubmit();
    expect(authServiceMock.signUp).not.toHaveBeenCalled();
  });

  it('should navigate to sign-in page on successful authentication', () => {
    authServiceMock.signUp.and.returnValue(of( { }));
    component.ngOnInit();
    component.signupForm.setValue({ username: 'test', email: 'test@gmail.com', password: 'password', c_password: 'password', updateOn: 'blur' });
    component.onSubmit();
    expect(routerMock.navigate).toHaveBeenCalledWith(['sign-in']);
  });

  it('should validate username', () => {
    component.ngOnInit();
    const username = component.signupForm.controls['username'];
    username.setValue('validUsername');
    expect(username.valid).toBeTruthy();

    username.setValue('v'); // too short
    expect(username.valid).toBeFalsy();
    username.setValue(''); // empty
    expect(username.valid).toBeFalsy();
  });

  it('should validate email', () => {
    component.ngOnInit();
    const email = component.signupForm.controls['email'];
    email.setValue('validEmail@example.com');
    expect(email.valid).toBeTruthy();
    email.setValue('a@e.c');
    expect(email.valid).toBeTruthy();
    email.setValue('validEmail@example.');
    expect(email.valid).toBeFalsy();
    email.setValue('invalidEmail'); // not a valid email
    expect(email.valid).toBeFalsy();
    email.setValue(''); // empty
    expect(email.valid).toBeFalsy();
  });

  it('should validate password', () => {
    component.ngOnInit();
    const password = component.signupForm.controls['password'];
    password.setValue('validPassword123');
    expect(password.valid).toBeTruthy();

    password.setValue('short'); // too short
    expect(password.valid).toBeFalsy();
    password.setValue(''); // empty
    expect(password.valid).toBeFalsy();
  });

  it('should validate c_password', () => {
    component.ngOnInit();
    const password = component.signupForm.controls['password'];
    const c_password = component.signupForm.controls['c_password'];
    password.setValue('validPassword123');
    c_password.setValue('validPassword123'); // same as password
    expect(c_password.valid).toBeTruthy();

    c_password.setValue('differentPassword'); // different from password
    expect(c_password.valid).toBeFalsy();
  });
});
