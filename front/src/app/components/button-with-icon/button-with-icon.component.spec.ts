import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ButtonWithIconComponent } from './button-with-icon.component';

describe('ButtonWithIconComponent', () => {
  let component: ButtonWithIconComponent;
  let fixture: ComponentFixture<ButtonWithIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ButtonWithIconComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ButtonWithIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
