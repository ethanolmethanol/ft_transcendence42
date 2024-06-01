import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnlineGameSelectorPageComponent } from './online-game-selector-page.component';

describe('OnlineGameSelectorPageComponent', () => {
  let component: OnlineGameSelectorPageComponent;
  let fixture: ComponentFixture<OnlineGameSelectorPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OnlineGameSelectorPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OnlineGameSelectorPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
