import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CPasswordErrorComponent } from './c-password-error.component';

describe('CPasswordErrorComponent', () => {
  let component: CPasswordErrorComponent;
  let fixture: ComponentFixture<CPasswordErrorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CPasswordErrorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CPasswordErrorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
