import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaddleComponent } from './paddle.component';

describe('PaddleComponent', () => {
  let component: PaddleComponent;
  let fixture: ComponentFixture<PaddleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PaddleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PaddleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
