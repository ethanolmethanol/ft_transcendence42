import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GamePageComponent } from './game-page.component';

describe('GamePageComponent', () => {
  let component: GamePageComponent;
  let fixture: ComponentFixture<GamePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GamePageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GamePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should update game container scale', () => {
    const gameContainer = fixture.debugElement.nativeElement.querySelector('.game-container');

    // Mock window dimensions
    spyOnProperty(window, 'innerWidth').and.returnValue(500);
    spyOnProperty(window, 'innerHeight').and.returnValue(500);

    (component as any).updateGameContainerScale();
    expect(gameContainer.style.transform).toBe('scale(0.5)');
  });

  it('should update game container scale', () => {
    const gameContainer = fixture.debugElement.nativeElement.querySelector('.game-container');

    // Mock window dimensions
    spyOnProperty(window, 'innerWidth').and.returnValue(300);
    spyOnProperty(window, 'innerHeight').and.returnValue(500);

    (component as any).updateGameContainerScale();
    expect(gameContainer.style.transform).toBe('scale(0.3)');
  });

  it('should update game container scale', () => {
    const gameContainer = fixture.debugElement.nativeElement.querySelector('.game-container');

    // Mock window dimensions
    spyOnProperty(window, 'innerWidth').and.returnValue(300);
    spyOnProperty(window, 'innerHeight').and.returnValue(10);

    (component as any).updateGameContainerScale();
    expect(gameContainer.style.transform).toBe('scale(0.01)');
  });

  it('should navigate to home page on confirm give up', () => {
    spyOn(window, 'confirm').and.returnValue(true);
    const navigateSpy = spyOn((component as any).router, 'navigate');
    component.confirmGiveUp();
    expect(navigateSpy).toHaveBeenCalledWith(['/home']);
  });
});
