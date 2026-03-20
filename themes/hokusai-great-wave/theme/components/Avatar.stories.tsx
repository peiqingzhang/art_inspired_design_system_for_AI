import type { Meta, StoryObj } from '@storybook/react';
import Avatar from './Avatar';

const meta  : Meta<typeof Avatar> = {
  title: 'Components/Avatar',
  component: Avatar,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Avatar>;

export const Initials: Story = { args={{ name: 'Ada Lovelace' }} };
export const Image: Story = { args={{ name: 'Ada Lovelace', src: 'https://i.pravatar.cc/80' }} };
