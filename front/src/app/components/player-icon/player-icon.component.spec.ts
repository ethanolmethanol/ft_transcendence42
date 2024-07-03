import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerIconComponent } from './player-icon.component';

describe('PlayerIconComponent', () => {
  let component: PlayerIconComponent;
  let fixture: ComponentFixture<PlayerIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerIconComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PlayerIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
