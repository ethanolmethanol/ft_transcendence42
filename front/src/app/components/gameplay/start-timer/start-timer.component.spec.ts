import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StartTimerComponent } from './start-timer.component';

describe('StartTimerComponent', () => {
  let component: StartTimerComponent;
  let fixture: ComponentFixture<StartTimerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StartTimerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StartTimerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
