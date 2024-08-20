import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameComponent } from './game.component';
import {PaddleComponent} from "../paddle/paddle.component";
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { WebSocketService } from '../../../services/web-socket/web-socket.service';

describe('GameComponent', () => {
  let component: GameComponent;
  let fixture: ComponentFixture<GameComponent>;
  let webSocketService: WebSocketService;
  let sendPaddleMovementSpy: jasmine.Spy;

  beforeEach(async () => {
      await TestBed.configureTestingModule({
        imports: [HttpClientTestingModule, GameComponent, PaddleComponent],
        providers: [WebSocketService]
      }).compileComponents();

      fixture = TestBed.createComponent(GameComponent);
      component = fixture.componentInstance;
      fixture.detectChanges();
      webSocketService = TestBed.inject(WebSocketService);
      sendPaddleMovementSpy = spyOn(webSocketService, 'sendPaddleMovement').and.callThrough();
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

  it('should move paddle up on pressed keys', () => {
    const event = new KeyboardEvent('keydown', { key: 'w' });
    window.dispatchEvent(event);
    component['gameLoop']();
    expect(sendPaddleMovementSpy).toHaveBeenCalledWith("Player1", -1);
 });

 it('should move paddle down on pressed keys', () => {
    const event = new KeyboardEvent('keydown', { key: 's' });
    window.dispatchEvent(event);
    component['gameLoop']();
    expect(sendPaddleMovementSpy).toHaveBeenCalledWith("Player1", 1);
 });

  it('should call movePaddle for each paddle in gameLoop', () => {
    spyOn(component as any, 'movePaddle');
    component['gameLoop']();
    expect((component as any).movePaddle).toHaveBeenCalledTimes(2); // Assuming there are 2 paddles
  });
});
