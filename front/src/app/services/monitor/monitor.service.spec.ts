import { TestBed } from '@angular/core/testing';

import { MonitorService } from './monitor.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('MonitorService', () => {
  let service: MonitorService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(MonitorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
