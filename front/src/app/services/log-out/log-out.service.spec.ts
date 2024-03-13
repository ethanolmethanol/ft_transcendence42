import { TestBed } from '@angular/core/testing';

import { LogoutService } from './log-out.service';

describe('LogOutService', () => {
  let service: LogoutService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LogoutService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
