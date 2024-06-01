import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from './auth.service';
import {API_AUTH} from "../../constants";

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Ensure that there are no outstanding requests
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('signIn should send a POST request', () => {
    const loginResponse = { detail: 'Success' };
    service.signIn('test', 'test').subscribe(response => {
      expect(response).toEqual(loginResponse);
    });

    const req = httpMock.expectOne(`${API_AUTH}/signin/`);
    expect(req.request.method).toBe('POST');
    req.flush(loginResponse);
  });

  it('signUp should send a POST request', () => {
    const signUpResponse = { detail: 'Success' };
    service.signUp('test', 'test@test.com', 'test').subscribe(response => {
      expect(response).toEqual(signUpResponse);
    });

    const req = httpMock.expectOne(`${API_AUTH}/signup/`);
    expect(req.request.method).toBe('POST');
    req.flush(signUpResponse);
  });

  it('isLoggedIn should send a GET request', () => {
    service.isLoggedIn().subscribe(response => {
      expect(response).toBeTrue();
    });

    const req = httpMock.expectOne(`${API_AUTH}/is_logged/`);
    expect(req.request.method).toBe('GET');
    req.flush({}, { status: 200, statusText: 'OK' });
  });

  it('logout should send a POST request', () => {
    service.logout();

    const req = httpMock.expectOne(`${API_AUTH}/logout/`);
    expect(req.request.method).toBe('POST');
    req.flush({});
  });
});
