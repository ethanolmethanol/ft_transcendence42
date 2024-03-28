import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsernameErrorComponent } from './username-error.component';

describe('UsernameErrorComponent', () => {
  let component: UsernameErrorComponent;
  let fixture: ComponentFixture<UsernameErrorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UsernameErrorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UsernameErrorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
