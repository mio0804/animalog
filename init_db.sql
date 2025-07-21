-- Drop existing tables if they exist
DROP TABLE IF EXISTS diaries CASCADE;
DROP TABLE IF EXISTS pets CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cognito_sub VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create pets table
CREATE TABLE pets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50),
    breed VARCHAR(100),
    birth_date DATE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create diaries table
CREATE TABLE diaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pet_id UUID NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_pets_user_id ON pets(user_id);
CREATE INDEX idx_diaries_pet_id ON diaries(pet_id);
CREATE INDEX idx_diaries_user_id ON diaries(user_id);
CREATE INDEX idx_diaries_created_at ON diaries(created_at DESC);

-- Insert test data for development
INSERT INTO users (cognito_sub, email, username) VALUES 
    ('test-user-123', 'test@example.com', 'テスト');

-- Get the test user ID
DO $$
DECLARE
    test_user_id UUID;
    test_pet_id UUID;
BEGIN
    SELECT id INTO test_user_id FROM users WHERE cognito_sub = 'test-user-123';
    
    -- Insert test pets
    INSERT INTO pets (user_id, name, species, breed, birth_date, description) VALUES 
        (test_user_id, 'ポチ', '犬', '柴犬', '2020-05-15', '元気いっぱいの柴犬です')
    RETURNING id INTO test_pet_id;
    
    INSERT INTO pets (user_id, name, species, breed, birth_date, description) VALUES 
        (test_user_id, 'タマ', '猫', 'スコティッシュフォールド', '2019-03-10', 'おとなしい性格の猫です');
    
    -- Insert test diaries for the first pet
    INSERT INTO diaries (pet_id, user_id, title, content, image_url) VALUES 
        (test_pet_id, test_user_id, '今日のお散歩', '今日は公園でたくさん遊びました！', NULL),
        (test_pet_id, test_user_id, 'お昼寝タイム', 'ずっと寝ていました。かわいい寝顔です。', NULL);
END $$;