import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmailErrorComponent } from './email-error.component';

describe('EmailErrorComponent', () => {
  let component: EmailErrorComponent;
  let fixture: ComponentFixture<EmailErrorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmailErrorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EmailErrorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
