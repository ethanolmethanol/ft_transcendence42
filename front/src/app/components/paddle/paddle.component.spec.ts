import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaddleComponent } from './paddle.component';
import {GAME_HEIGHT, PADDLE_HEIGHT} from "../../constants";

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

  it('should stay within game after moving up', () => {
    component.speed = 1000;
    component.moveUp();
    expect(component.positionY).toBeGreaterThanOrEqual(0);
  });

  it('should stay within game after moving down', () => {
    component.speed = 1000;
    component.moveDown();
    expect(component.positionY).toBeLessThanOrEqual(GAME_HEIGHT - PADDLE_HEIGHT);
  });
});
