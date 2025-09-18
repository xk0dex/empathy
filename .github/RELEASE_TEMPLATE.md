# Release Template for Empathy

## Pre-Release Checklist

### Technical Requirements
- [ ] All tests passing (unit, integration, advanced)
- [ ] Security audit completed
- [ ] Performance benchmarks validated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated with new version

### Version Management
- [ ] Version bumped in `src/__version__.py`
- [ ] Git tag created with semantic versioning
- [ ] Release notes written in `RELEASE_NOTES_v{VERSION}.md`

### Quality Gates
- [ ] Code coverage > 80%
- [ ] No critical security vulnerabilities
- [ ] Multi-language support tested
- [ ] Large repository performance validated (1000+ commits)

### GitHub Release Process
- [ ] Tag pushed to repository
- [ ] GitHub Release created with notes
- [ ] Assets attached (if any)
- [ ] Release marked as latest/pre-release appropriately

## Release Notes Template

### Version X.Y.Z - "Release Name"

**Release Date:** YYYY-MM-DD

#### 🚀 New Features
- Feature description

#### 🐛 Bug Fixes  
- Bug fix description

#### 🔧 Improvements
- Improvement description

#### 📚 Documentation
- Documentation updates

#### ⚡ Performance
- Performance optimizations

#### 🔒 Security
- Security enhancements

#### 🌍 Localization
- Multi-language support updates

### Breaking Changes
- Any breaking changes

### Migration Guide
- How to migrate from previous version

### Known Issues
- Any known limitations or issues

### Contributors
- List of contributors for this release