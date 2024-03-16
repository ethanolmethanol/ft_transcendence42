import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PasswordErrorComponent } from './password-error.component';

describe('PasswordErrorComponent', () => {
  let component: PasswordErrorComponent;
  let fixture: ComponentFixture<PasswordErrorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PasswordErrorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PasswordErrorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
