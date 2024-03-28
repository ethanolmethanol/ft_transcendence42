import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameComponent } from './game.component';
import {By} from "@angular/platform-browser";
import {PaddleComponent} from "../paddle/paddle.component";

describe('GameComponent', () => {
  let component: GameComponent;
  let fixture: ComponentFixture<GameComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GameComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have exactly 2 paddles', () => {
    expect(component.paddles.length).toEqual(2);
  });

  it('should have exactly 1 ball', () => {
    expect(component.ball).toBeTruthy();
  });

  it('should add key to pressedKeys set on keydown', () => {
    const event = new KeyboardEvent('keydown', { key: 'w' });
    window.dispatchEvent(event);
    expect(component['pressedKeys'].has('w')).toBeTrue();
  });

  it('should remove key from pressedKeys set on keyup', () => {
    const event = new KeyboardEvent('keyup', { key: 'w' });
    window.dispatchEvent(event);
    expect(component['pressedKeys'].has('w')).toBeFalse();
  });

  it('should move paddle up or down based on pressed keys', () => {
    const paddle = fixture.debugElement.query(By.directive(PaddleComponent)).injector.get(PaddleComponent);
    spyOn(paddle, 'moveUp');
    spyOn(paddle, 'moveDown');

    component['pressedKeys'].add('w');
    component['pressedKeys'].add('s');
    component['movePaddle'](paddle, { upKey: 'w', downKey: 's' });
    expect(paddle.moveUp).not.toHaveBeenCalled();
    expect(paddle.moveDown).not.toHaveBeenCalled();
    component['pressedKeys'].delete('s');
    component['movePaddle'](paddle, { upKey: 'w', downKey: 's' });
    expect(paddle.moveUp).toHaveBeenCalled();
    expect(paddle.moveDown).not.toHaveBeenCalled();

    component['pressedKeys'].delete('w');
    component['pressedKeys'].add('s');
    component['movePaddle'](paddle, { upKey: 'w', downKey: 's' });
    expect(paddle.moveDown).toHaveBeenCalled();
  });

  it('should call movePaddle for each paddle in gameLoop', () => {
    spyOn(component as any, 'movePaddle');
    component['gameLoop']();
    expect((component as any).movePaddle).toHaveBeenCalledTimes(2); // Assuming there are 2 paddles
  });
});
