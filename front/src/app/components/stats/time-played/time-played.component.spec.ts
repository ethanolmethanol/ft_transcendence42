import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimePlayedComponent } from './time-played.component';

describe('TimePlayedComponent', () => {
  let component: TimePlayedComponent;
  let fixture: ComponentFixture<TimePlayedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TimePlayedComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TimePlayedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
