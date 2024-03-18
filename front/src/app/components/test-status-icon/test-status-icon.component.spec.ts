import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestStatusIconComponent } from './test-status-icon.component';

describe('TestStatusIconComponent', () => {
  let component: TestStatusIconComponent;
  let fixture: ComponentFixture<TestStatusIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestStatusIconComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TestStatusIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
