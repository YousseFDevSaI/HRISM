import { TestBed } from '@angular/core/testing';

import { GlobalvService } from './globalv.service';

describe('GlobalvService', () => {
  let service: GlobalvService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GlobalvService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
