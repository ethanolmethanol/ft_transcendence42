import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ColorWheelComponent } from './color-wheel.component';

describe('ColorWheelComponent', () => {
  let component: ColorWheelComponent;
  let fixture: ComponentFixture<ColorWheelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ColorWheelComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ColorWheelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
